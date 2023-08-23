import filecmp
import os
from .edalize_common import make_edalize_test, tests_dir


def test_questa_formal(make_edalize_test):
    tool_options = {
        "vcom_options": ["various", "vcom_options"],
        "vlog_options": ["some", "vlog_options"],
        "qverify_options": ["a", "few", "qverify_options"],
        "qverify_do_files": ["edalize_autocheck.tcl", "waiver_module_0.tcl", "waiver_module_1.tcl"],
    }

    # FIXME: Add VPI tests
    tf = make_edalize_test("questaformal", tool_options=tool_options)

    tf.backend.configure()

    tf.compare_files(["Makefile", "edalize_build_rtl.tcl", "edalize_main.tcl"])

    orig_env = os.environ.copy()
    try:
        # os.environ["MODEL_TECH"] = os.path.join(tests_dir, "mock_commands")

        tf.backend.build()
        os.makedirs(os.path.join(tf.work_root, "work"))

        tf.compare_files(["qverify.cmd"])

        tf.backend.run()

        assert filecmp.cmp(
            os.path.join(tf.ref_dir, "qverify2.cmd"),
            os.path.join(tf.work_root, "qverify.cmd"),
            shallow=False,
        )
    finally:
        os.environ = orig_env


def test_questa_formal_autocheck(tmpdir):

    from edalize.edatool import get_edatool

    from .edalize_common import compare_files, tests_dir

    os.environ["PATH"] = (
        os.path.join(tests_dir, "mock_commands") + ":" + os.environ["PATH"]
    )

    tool = "questaformal"
    tool_options = {
        "vcom_options": ["various", "vcom_options"],
        "vlog_options": ["some", "vlog_options"],
        "qverify_options": ["a", "few", "qverify_options"],
        "qverify_do_files": ["edalize_autocheck.tcl",],
        "autocheck_options": ["a", "few", "autocheck_options"],
    }

    name = "test_{}_autocheck0".format(tool)
    work_root = str(tmpdir)
    edam = {"name": name, "tool_options": {tool: tool_options}}

    backend = get_edatool(tool)(edam=edam, work_root=work_root)
    backend.configure()

    ref_dir = os.path.join(tests_dir, "test_" + tool, "autocheck")
    compare_files(
        ref_dir,
        work_root,
        #["Makefile", "edalize_build_rtl.tcl", "edalize_main.tcl", "edalize_autocheck.tcl"]
        ["Makefile", "edalize_main.tcl", "edalize_autocheck.tcl",]
    )

    #backend.build()
